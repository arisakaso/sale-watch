type Props = {
  status: string;
};

export default function StatusBadge({ status }: Props) {
  const { bg, text, ring } = colorByStatus(status);

  return (
    <span
      className={[
        "inline-flex items-center rounded-full px-2.5 py-0.5",
        "text-xs font-medium",
        "ring-1 ring-inset",
        bg,
        text,
        ring,
      ].join(" ")}
    >
      {status}
    </span>
  );
}

function colorByStatus(status: string) {
  // 日本語ステータスに基づいて色を割り当て
  switch (status) {
    case "受付中":
      return {
        bg: "bg-green-100 dark:bg-green-900/30",
        text: "text-green-800 dark:text-green-300",
        ring: "ring-green-300/60 dark:ring-green-700/60",
      } as const;
    case "予定":
      return {
        bg: "bg-amber-100 dark:bg-amber-900/30",
        text: "text-amber-800 dark:text-amber-300",
        ring: "ring-amber-300/60 dark:ring-amber-700/60",
      } as const;
    case "終了":
      return {
        bg: "bg-gray-100 dark:bg-gray-800",
        text: "text-gray-700 dark:text-gray-300",
        ring: "ring-gray-300/60 dark:ring-gray-700/60",
      } as const;
    default:
      return {
        bg: "bg-foreground/10",
        text: "text-foreground",
        ring: "ring-foreground/20",
      } as const;
  }
}
