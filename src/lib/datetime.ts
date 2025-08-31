// 日付文字列(ISOなど)を日本向けの見やすい形式に整形
// 例: 2025/09/10(水) 23:59
export function formatJPDateTime(value: string | null | undefined): string {
  if (!value) return "未定";
  const d = new Date(value);
  if (isNaN(d.getTime())) return "—";

  const fmt = new Intl.DateTimeFormat("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    weekday: "short",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: "Asia/Tokyo",
  });

  return fmt.format(d);
}

