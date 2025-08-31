This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Supabase 連携の準備

本リポジトリには Supabase クライアント（`@supabase/supabase-js`）の導入と、サーバー側から予約情報を取得する関数を用意しています。以下の手順でローカル接続を設定できます。

1) 環境変数を設定

```bash
cp .env.example .env.local
# `.env.local` を編集して以下を設定
# SUPABASE_URL=あなたのプロジェクトURL
# SUPABASE_ANON_KEY=Anonキー
```

2) テーブル作成（Supabase SQL Editor）

```sql
create table if not exists reservations (
  id uuid primary key default gen_random_uuid(),
  item text not null,
  status text not null,
  deadline timestamptz null,
  link text not null
);

-- RLS を有効化し、公開読み取りを許可
alter table reservations enable row level security;
create policy "public read reservations" on reservations
  for select using (true);
```

3) 起動して確認

```bash
npm run dev
```

トップページ（`/`）で「予約情報」テーブルに Supabase のデータが表示されます。環境変数が未設定の場合は、ダミーデータが表示されます。

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
