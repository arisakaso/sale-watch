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

// 期限が現在時刻より過去かどうか
export function isPast(value: string | null | undefined): boolean {
  if (!value) return false;
  const d = new Date(value);
  if (isNaN(d.getTime())) return false;
  return d.getTime() < Date.now();
}

// 現在からの相対時間（ざっくり、日本語）
// 例: 「あと3日」「あと2時間」「あと15分」「締切済み」
export function relativeFromNowJP(value: string | null | undefined): string {
  if (!value) return "未定";
  const d = new Date(value);
  if (isNaN(d.getTime())) return "—";

  const diffMs = d.getTime() - Date.now();
  if (diffMs < 0) return "締切済み";

  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;

  if (diffMs < minute) return "まもなく";
  if (diffMs < hour) return `あと${Math.floor(diffMs / minute)}分`;
  if (diffMs < day) return `あと${Math.floor(diffMs / hour)}時間`;
  return `あと${Math.floor(diffMs / day)}日`;
}
