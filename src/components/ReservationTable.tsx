import { Reservation } from "@/types/reservation";
import { formatJPDateTime, isPast, relativeFromNowJP } from "@/lib/datetime";
import StatusBadge from "@/components/StatusBadge";

type Props = {
  data: Reservation[];
};

export default function ReservationTable({ data }: Props) {
  return (
    <div className="rounded-lg border border-foreground/10 overflow-x-auto">
      <table className="w-full border-collapse text-sm sm:text-base">
        <thead>
          <tr className="bg-foreground/5">
            <th scope="col" className="text-left px-4 py-2">
              アイテム
            </th>
            <th scope="col" className="text-left px-4 py-2">
              ステータス
            </th>
            <th scope="col" className="text-left px-4 py-2 whitespace-nowrap">
              締切
            </th>
            <th scope="col" className="text-left px-4 py-2">
              リンク
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => {
            const expired = isPast(row.deadline);
            return (
              <tr key={row.id} className={expired ? "opacity-60" : undefined}>
                <td className="px-4 py-2 border-t border-foreground/10">{row.item}</td>
                <td className="px-4 py-2 border-t border-foreground/10">
                  <StatusBadge status={row.status} />
                </td>
                <td className="px-4 py-2 border-t border-foreground/10 whitespace-nowrap">
                  <div>{formatJPDateTime(row.deadline)}</div>
                  <div className="text-xs text-foreground/70">{relativeFromNowJP(row.deadline)}</div>
                </td>
                <td className="px-4 py-2 border-t border-foreground/10">
                  <a
                    href={row.link}
                    className="hover:underline text-foreground"
                    target="_blank"
                    rel="noreferrer"
                  >
                    詳細
                  </a>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
