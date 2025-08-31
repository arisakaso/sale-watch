import ReservationTable from "@/components/ReservationTable";
import { fetchReservations } from "@/lib/supabase/server";

export default async function Home() {
  const reservations = await fetchReservations();

  return (
    <main className="min-h-screen p-8 sm:p-20">
      <div className="w-full max-w-4xl mx-auto space-y-8">
        <h1 className="text-4xl sm:text-6xl font-bold tracking-tight text-foreground">
          Sale-Watch
        </h1>

        <section aria-labelledby="reservation-heading" className="space-y-3">
          <h2 id="reservation-heading" className="text-xl sm:text-2xl font-semibold">
            予約情報
          </h2>

          <ReservationTable data={reservations} />
        </section>
      </div>
    </main>
  );
}
