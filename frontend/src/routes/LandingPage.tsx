import React from "react";
import { motion } from "framer-motion";
import { Search, Code2, GitBranch, ArrowRight, BookOpen, Layers } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

const NAV_LINKS = ["Features", "Philosophy", "Documentation"];

export function LandingPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col font-sans selection:bg-blue-accent/20 selection:text-blue-accent">
      
      {/* Floating Navigation Bar */}
      <motion.nav 
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
        className="fixed top-0 inset-x-0 z-50 h-16 border-b border-border/50 bg-background/80 backdrop-blur-md flex items-center justify-between px-6 lg:px-12"
      >
        <div className="flex items-center gap-2 font-mono font-semibold tracking-tight text-lg">
          <div className="w-6 h-6 rounded bg-foreground text-background flex items-center justify-center text-xs">C</div>
          CodeMind
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
          {NAV_LINKS.map(link => (
            <a key={link} href={`#${link.toLowerCase()}`} className="hover:text-foreground transition-colors">
              {link}
            </a>
          ))}
        </div>
        <div className="flex items-center gap-4">
          <Button variant="ghost" asChild className="hidden sm:inline-flex">
            <Link to="/login">Sign In</Link>
          </Button>
          <Button variant="primary" asChild>
            <Link to="/register">Get Started</Link>
          </Button>
        </div>
      </motion.nav>

      <main className="flex-1 flex flex-col items-center w-full pt-32 pb-24 px-6 lg:px-12 max-w-[1400px] mx-auto">
        
        {/* Hero Section */}
        <section className="flex flex-col items-center text-center max-w-3xl w-full mb-24">
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.2, ease: "easeOut", delay: 0.1 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-muted text-xs font-medium text-muted-foreground mb-8"
          >
            <span className="w-2 h-2 rounded-full bg-blue-accent"></span>
            CodeMind 1.0 is now available
          </motion.div>
          <motion.h1 
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.2, ease: "easeOut", delay: 0.15 }}
            className="text-5xl sm:text-6xl md:text-7xl font-medium tracking-tight text-foreground mb-6"
          >
            Understand codebase logic instantly.
          </motion.h1>
          <motion.p 
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.2, ease: "easeOut", delay: 0.2 }}
            className="text-lg sm:text-xl text-muted-foreground max-w-2xl mb-10 leading-relaxed"
          >
            A premium retrieval-augmented tool that treats your repositories as knowledge bases. Ask questions, receive cited answers, and navigate complex architectures without losing context.
          </motion.p>
          <motion.div 
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.2, ease: "easeOut", delay: 0.25 }}
            className="flex flex-col sm:flex-row items-center gap-4 w-full justify-center"
          >
            <Button variant="primary" size="lg" className="w-full sm:w-auto">
              Start Building <ArrowRight className="ml-2 size-4" />
            </Button>
            <Button variant="outline" size="lg" className="w-full sm:w-auto">
              Read the Docs
            </Button>
          </motion.div>
        </section>

        {/* Interactive Product Preview (Mock App Window) */}
        <motion.section 
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.22, ease: "easeOut", delay: 0.3 }}
          className="w-full max-w-5xl rounded-xl border border-border bg-background mock-window-shadow overflow-hidden flex flex-col md:flex-row h-[600px] mb-32"
        >
          {/* Sidebar */}
          <div className="w-full md:w-64 border-r border-border bg-muted/30 flex flex-col">
            <div className="h-12 border-b border-border flex items-center px-4 text-xs font-mono font-medium text-muted-foreground">
              EXPLORER
            </div>
            <div className="flex-1 p-3 overflow-y-auto">
              <div className="flex flex-col gap-1 text-sm font-mono text-muted-foreground">
                <div className="flex items-center gap-2 px-2 py-1.5 hover:bg-muted rounded cursor-pointer transition-colors">
                  <Search className="size-3.5" /> search
                </div>
                <div className="flex items-center gap-2 px-2 py-1.5 hover:bg-muted rounded cursor-pointer transition-colors">
                  <GitBranch className="size-3.5" /> main
                </div>
                <div className="mt-4 mb-2 px-2 text-xs font-sans font-semibold text-foreground/50">REPOSITORY</div>
                <div className="flex items-center gap-2 px-2 py-1.5 bg-blue-accent/10 text-blue-accent rounded cursor-default">
                  <Code2 className="size-3.5" /> main.tsx
                </div>
                <div className="flex items-center gap-2 px-2 py-1.5 hover:bg-muted rounded cursor-pointer transition-colors">
                  <Code2 className="size-3.5" /> App.tsx
                </div>
                <div className="flex items-center gap-2 px-2 py-1.5 hover:bg-muted rounded cursor-pointer transition-colors">
                  <BookOpen className="size-3.5" /> utils.ts
                </div>
              </div>
            </div>
          </div>
          
          {/* Main Area */}
          <div className="flex-1 flex flex-col bg-background">
            <div className="h-12 border-b border-border flex items-center px-4 gap-4 overflow-x-auto scrollbar-hide">
              <div className="flex items-center gap-2 text-sm font-mono text-foreground border-b-2 border-blue-accent h-full pt-[2px]">
                Ask CodeMind
              </div>
            </div>
            <div className="flex-1 p-6 overflow-y-auto flex flex-col gap-6">
              {/* Mock Chat / Interaction */}
              <div className="flex flex-col gap-2 max-w-2xl">
                <div className="flex items-center gap-3">
                  <div className="w-7 h-7 rounded-full bg-muted flex items-center justify-center text-xs font-medium">U</div>
                  <span className="font-medium text-sm">User</span>
                </div>
                <div className="pl-10 text-sm text-muted-foreground">
                  Where is the authentication state managed in this React application?
                </div>
              </div>

              <div className="flex flex-col gap-3 max-w-2xl mt-4">
                <div className="flex items-center gap-3">
                  <div className="w-7 h-7 rounded bg-foreground text-background flex items-center justify-center text-xs font-medium">C</div>
                  <span className="font-medium text-sm">CodeMind</span>
                </div>
                <div className="pl-10 text-sm leading-relaxed text-foreground space-y-4">
                  <p>The authentication state is managed globally using Zustand in the <span className="px-1.5 py-0.5 rounded bg-muted font-mono text-xs text-muted-foreground border border-border">store/auth.ts</span> file.</p>
                  <div className="p-4 rounded-md border border-border bg-muted/30 font-mono text-xs overflow-x-auto text-muted-foreground">
                    <span className="text-blue-accent">export</span> <span className="text-foreground">const</span> useAuth = create&lt;AuthState&gt;((set) =&gt; (&#123;<br/>
                    &nbsp;&nbsp;user: <span className="text-blue-accent">null</span>,<br/>
                    &nbsp;&nbsp;isAuthenticated: <span className="text-blue-accent">false</span>,<br/>
                    &nbsp;&nbsp;login: (user) =&gt; set(&#123; user, isAuthenticated: <span className="text-blue-accent">true</span> &#125;),<br/>
                    &nbsp;&nbsp;logout: () =&gt; set(&#123; user: <span className="text-blue-accent">null</span>, isAuthenticated: <span className="text-blue-accent">false</span> &#125;),<br/>
                    &#125;))
                  </div>
                  <p>It is then consumed by the <span className="px-1.5 py-0.5 rounded bg-muted font-mono text-xs text-muted-foreground border border-border">ProtectedRoute.tsx</span> component to guard private routes.</p>
                </div>
              </div>
            </div>
            
            <div className="p-4 border-t border-border">
              <div className="w-full rounded-md border border-border bg-muted/30 px-4 py-3 flex items-center text-sm text-muted-foreground font-mono">
                Ask a follow up question...
              </div>
            </div>
          </div>
        </motion.section>

        {/* Features Section */}
        <section id="features" className="w-full max-w-5xl mb-32">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <FeatureCard 
              icon={<Search className="size-5" />}
              title="Semantic Retrieval"
              description="Instantly find relevant code snippets and architecture references without relying on exact string matches."
            />
            <FeatureCard 
              icon={<Layers className="size-5" />}
              title="Contextual Understanding"
              description="CodeMind analyzes relationships between files, providing holistic answers rather than isolated code chunks."
            />
            <FeatureCard 
              icon={<GitBranch className="size-5" />}
              title="Version Aware"
              description="Stays in sync with your latest commits, ensuring answers are always based on the current state of your repository."
            />
          </div>
        </section>

        {/* Philosophy Section */}
        <section id="philosophy" className="w-full max-w-3xl text-center mb-32 flex flex-col items-center">
          <h2 className="text-3xl font-medium tracking-tight mb-6">Designed for engineers.</h2>
          <p className="text-muted-foreground leading-relaxed text-lg mb-8">
            We built CodeMind because modern codebases are vast, complex, and constantly evolving. 
            Traditional search tools are insufficient, and generalized chat models lack repository context. 
            CodeMind bridges this gap by providing accurate, cited, and deeply contextual answers directly from your codebase. 
            No buzzwords. Just better developer tooling.
          </p>
          <Button variant="outline">Read our manifesto</Button>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-background py-12 px-6 lg:px-12 text-sm text-muted-foreground">
        <div className="max-w-[1400px] mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 font-mono font-medium">
            <div className="w-5 h-5 rounded bg-muted flex items-center justify-center text-[10px] text-foreground">C</div>
            CodeMind
          </div>
          <div className="flex items-center gap-6">
            <a href="#" className="hover:text-foreground transition-colors">Twitter</a>
            <a href="#" className="hover:text-foreground transition-colors">GitHub</a>
            <a href="#" className="hover:text-foreground transition-colors">Terms</a>
            <a href="#" className="hover:text-foreground transition-colors">Privacy</a>
          </div>
          <div>&copy; {new Date().getFullYear()} CodeMind Inc. All rights reserved.</div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <motion.div 
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className="flex flex-col gap-4 p-6 rounded-xl border border-border bg-background shadow-sm hover:shadow-md transition-shadow"
    >
      <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center text-foreground">
        {icon}
      </div>
      <h3 className="text-lg font-medium tracking-tight text-foreground">{title}</h3>
      <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
    </motion.div>
  )
}
