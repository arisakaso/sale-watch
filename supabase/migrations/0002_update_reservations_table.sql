-- 破壊的変更: 既存の reservations テーブルを削除して再作成します。
-- 既存データは失われます（ダミーデータ想定）。

-- 1) 既存テーブルを削除（存在する場合）
drop table if exists reservations cascade;

-- 2) 新スキーマで作成
create table if not exists reservations (
  id uuid primary key default gen_random_uuid(),
  item text not null,
  vendor text not null,
  status text not null,
  entry_start_at timestamptz null,
  entry_end_at timestamptz null,
  lottery_at timestamptz null,
  sales_start_at timestamptz null,
  link text not null
);

-- 3) RLS を有効化し、公開読み取りを許可
alter table reservations enable row level security;
drop policy if exists "public read reservations" on reservations;
create policy "public read reservations" on reservations
  for select using (true);

-- 4) 並び替え用のインデックス（受付終了日）
create index if not exists idx_reservations_entry_end_at on reservations (entry_end_at);

-- 5) 動作確認用のダミーデータ
insert into reservations (item, vendor, status, entry_start_at, entry_end_at, lottery_at, sales_start_at, link) values
  ('RICOH GR IV 1次抽選', 'RICOH 公式', '受付中', '2025-09-01 10:00+09', '2025-09-10 23:59+09', '2025-09-12 12:00+09', '2025-09-20 10:00+09', 'https://example.com/1'),
  ('RICOH GR IV 2次抽選', '量販店A', '予定', null, null, null, null, 'https://example.com/2'),
  ('RICOH GR IV 先行予約', '量販店B', '終了', '2025-08-10 10:00+09', '2025-08-20 23:59+09', null, '2025-09-05 10:00+09', 'https://example.com/3');
