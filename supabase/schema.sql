create table public.assignments(
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references auth.users (id) on delete cascade,  
  course text not null, 
  assignment_name text not null,
  due_date date not null,  
  completed boolean not null default false,
  created_at timestamptz not null default now()
);

alter table public.assignments enable row level security;

grant select , insert, update, delete on public.assignments to authenticated;

create policy "users read own assignments" on public.assignments
  for select to authenticated
  using ((select auth.uid()) = user_id);

create policy "users add own assignments" on public.assignments
  for insert to authenticated
  with check ((select auth.uid()) = user_id);  

create policy "users change own assignments" on public.assignments
  for update to authenticated
  using ((select auth.uid()) = user_id)  
  with check ((select auth.uid()) = user_id);  

create policy "users delete own assignments" on public.assignments
  for delete to authenticated
  using ((select auth.uid()) = user_id);  