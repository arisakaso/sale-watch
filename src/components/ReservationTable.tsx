import { Reservation } from "@/types/reservation";
import { formatJPDateTime } from "@/lib/datetime";
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
          {data.map((row) => (
            <tr key={row.id}>
              <td className="px-4 py-2 border-t border-foreground/10">{row.item}</td>
              <td className="px-4 py-2 border-t border-foreground/10">
                <StatusBadge status={row.status} />
              </td>
              <td className="px-4 py-2 border-t border-foreground/10 whitespace-nowrap">
                {formatJPDateTime(row.deadline)}
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
          ))}
        </tbody>
      </table>
    </div>
  );
}
