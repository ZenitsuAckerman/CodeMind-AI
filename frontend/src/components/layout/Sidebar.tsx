
import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";
import { 
  Folder, 
  Settings, 
  LayoutDashboard, 
  FileText, 
  PanelLeftClose, 
  PanelLeftOpen 
} from "lucide-react";
import { useAppStore } from "@/store/appStore";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Projects", href: "/projects", icon: Folder },
  { name: "Documents", href: "/documents", icon: FileText },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const { isSidebarCollapsed, toggleSidebar } = useAppStore();

  return (
    <motion.aside
      initial={false}
      animate={{ width: isSidebarCollapsed ? 64 : 260 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className="hidden md:flex flex-col border-r border-border bg-muted/30 h-screen sticky top-0 shrink-0 z-40 overflow-hidden"
    >
      <div className="h-14 flex items-center justify-between px-4 border-b border-border shrink-0">
        {!isSidebarCollapsed && (
          <motion.div 
            initial={{ opacity: 0 }} 
            animate={{ opacity: 1 }} 
            exit={{ opacity: 0 }}
            className="flex items-center gap-2 font-mono font-medium truncate"
          >
            <div className="w-5 h-5 rounded bg-foreground text-background flex items-center justify-center text-[10px] shrink-0">C</div>
            CodeMind
          </motion.div>
        )}
        <Button 
          variant="ghost" 
          size="icon" 
          onClick={toggleSidebar} 
          className={cn("shrink-0", isSidebarCollapsed && "mx-auto")}
          title={isSidebarCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
        >
          {isSidebarCollapsed ? <PanelLeftOpen className="size-4" /> : <PanelLeftClose className="size-4" />}
        </Button>
      </div>

      <nav className="flex-1 flex flex-col gap-1 p-3 overflow-y-auto overflow-x-hidden">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.href}
              to={item.href}
              className={({ isActive }) => cn(
                "flex items-center gap-3 px-3 py-2 rounded-md transition-colors text-sm font-medium whitespace-nowrap",
                isActive 
                  ? "bg-blue-accent/10 text-blue-accent" 
                  : "text-muted-foreground hover:bg-muted hover:text-foreground",
                isSidebarCollapsed && "justify-center px-0"
              )}
              title={isSidebarCollapsed ? item.name : undefined}
            >
              <Icon className="size-4 shrink-0" />
              {!isSidebarCollapsed && <span>{item.name}</span>}
            </NavLink>
          );
        })}
      </nav>
      
      <div className="p-4 border-t border-border shrink-0">
        {!isSidebarCollapsed ? (
          <div className="bg-background rounded-lg border border-border p-3 text-xs">
            <div className="font-medium text-foreground mb-1">Workspace Limit</div>
            <div className="text-muted-foreground mb-2">3 / 5 projects used</div>
            <div className="w-full h-1.5 rounded-full bg-muted overflow-hidden">
              <div className="h-full bg-blue-accent w-[60%]" />
            </div>
          </div>
        ) : (
          <div className="w-full h-8 rounded bg-background border border-border flex items-center justify-center text-xs text-muted-foreground font-medium cursor-help" title="3/5 Projects">
            60%
          </div>
        )}
      </div>
    </motion.aside>
  );
}
