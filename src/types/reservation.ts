export type ReservationStatus = "受付中" | "予定" | "終了";

export interface Reservation {
  id: string;
  item: string;
  vendor: string;
  status: ReservationStatus | string;
  entryStartAt: string | null; // 受付開始日
  entryEndAt: string | null; // 受付終了日
  lotteryAt: string | null; // 抽選発表日
  salesStartAt: string | null; // 販売開始日
  link: string;
}
