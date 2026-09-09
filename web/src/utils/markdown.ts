import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'
import hljs from 'highlight.js/lib/core'
import { escapeHtml } from './format'

const md = new MarkdownIt({
  html: false, // 不允许 LLM 注入原始 HTML
  linkify: true,
  breaks: true, // 换行 -> <br>
  highlight(code: string, lang: string): string {
    let html = ''
    try {
      if (lang && hljs.getLanguage(lang)) {
        html = hljs.highlight(code, { language: lang, ignoreIllegals: true }).value
      } else {
        html = hljs.highlightAuto(code).value
      }
    } catch {
      html = escapeHtml(code)
    }
    return `<pre class="hljs md-code"><code>${html}</code></pre>`
  },
})

/** 把助手消息中的 Markdown 渲染为安全的 HTML（消毒后） */
export function renderMarkdown(text: string): string {
  if (!text) return ''
  const raw = md.render(text)
  return DOMPurify.sanitize(raw)
}
