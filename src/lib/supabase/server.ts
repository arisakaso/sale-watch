"use server";
import "server-only";
import { createClient } from "@supabase/supabase-js";
import type { Reservation } from "@/types/reservation";

// サーバー側で Supabase から予約情報を取得。
// 環境変数が未設定 or エラー時はダミーデータを返す。
export async function fetchReservations(): Promise<Reservation[]> {
  const url = process.env.SUPABASE_URL;
  const anon = process.env.SUPABASE_ANON_KEY;

  if (!url || !anon) {
    return DUMMY;
  }

  const supabase = createClient(url, anon);
  const { data, error } = await supabase
    .from("reservations")
    .select("id,item,status,deadline,link")
    .order("deadline", { ascending: true, nullsFirst: false });

  if (error) {
    console.error("Supabase fetch error:", error);
    return DUMMY;
  }

  // 型安全にしたければ Supabase の型生成（gen types）を導入する。
  return (data ?? []) as unknown as Reservation[];
}

const DUMMY: Reservation[] = [
  {
    id: "1",
    item: "RICOH GR IV 1次抽選",
    status: "受付中",
    deadline: "2025-09-10 23:59",
    link: "#",
  },
  {
    id: "2",
    item: "RICOH GR IV 2次抽選",
    status: "予定",
    deadline: null,
    link: "#",
  },
  {
    id: "3",
    item: "RICOH GR IV 先行予約",
    status: "終了",
    deadline: "2025-08-20 23:59",
    link: "#",
  },
];

