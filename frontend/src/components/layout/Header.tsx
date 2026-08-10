
import { Menu, Search } from "lucide-react";
import { useAppStore } from "@/store/appStore";
import { Breadcrumbs } from "@/components/navigation/Breadcrumbs";
import { ThemeToggle } from "@/components/shared/ThemeToggle";
import { ProfilePlaceholder } from "@/components/shared/ProfilePlaceholder";
import { Button } from "@/components/ui/button";

export function Header() {
  const { toggleSidebar, setCommandPaletteOpen } = useAppStore();

  return (
    <header className="h-14 border-b border-border bg-background flex items-center justify-between px-4 sticky top-0 z-30">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={toggleSidebar} className="md:hidden">
          <Menu className="size-4" />
        </Button>
        <Breadcrumbs />
      </div>
      
      <div className="flex items-center gap-2">
        <Button 
          variant="outline" 
          className="hidden sm:flex w-64 justify-between text-muted-foreground"
          onClick={() => setCommandPaletteOpen(true)}
        >
          <span className="inline-flex items-center gap-2">
            <Search className="size-4" />
            Search...
          </span>
          <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
            <span className="text-xs">⌘</span>K
          </kbd>
        </Button>
        <Button 
          variant="ghost" 
          size="icon" 
          className="sm:hidden"
          onClick={() => setCommandPaletteOpen(true)}
        >
          <Search className="size-4" />
        </Button>
        
        <ThemeToggle />
        <div className="w-px h-4 bg-border mx-1" />
        <ProfilePlaceholder initials="JD" />
      </div>
    </header>
  );
}
