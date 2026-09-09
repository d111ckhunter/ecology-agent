import hljs from 'highlight.js/lib/core'

export function highlightSql(sql: string): string {
  try {
    return hljs.highlight(sql, { language: 'sql' }).value
  } catch {
    return escapeHtml(sql)
  }
}

export function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

export function isPending(msg: { status?: string }): boolean {
  return msg.status !== undefined && msg.status !== 'done'
}
