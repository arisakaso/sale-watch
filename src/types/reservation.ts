export type ReservationStatus = "受付中" | "予定" | "終了";

export interface Reservation {
  id: string;
  item: string;
  status: ReservationStatus | string;
  deadline: string | null; // ISO文字列 or null
  link: string;
}

