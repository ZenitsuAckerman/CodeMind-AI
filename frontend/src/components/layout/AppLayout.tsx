
import { Outlet } from "react-router-dom";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { CommandPalette } from "@/components/search/CommandPalette";

export function AppLayout() {
  return (
    <div className="flex min-h-screen bg-background w-full">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header />
        <main className="flex-1 overflow-y-auto bg-muted/10 p-4 md:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
      <CommandPalette />
    </div>
  );
}
