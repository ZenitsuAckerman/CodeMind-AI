import { format } from "date-fns";
import { Folder, Trash2 } from "lucide-react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

import { useProjects, useDeleteProject, type Project } from "../api/projectService";
import { CreateProjectDialog } from "../components/CreateProjectDialog";
import { EmptyState } from "@/components/feedback/EmptyState";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export function Dashboard() {
  const { data: projects, isLoading, isError, refetch } = useProjects();
  const deleteProject = useDeleteProject();

  if (isLoading) {
    return <LoadingState message="Loading workspace projects..." />;
  }

  if (isError) {
    return <ErrorState message="Failed to load projects. Please ensure the backend is running." onRetry={() => refetch()} />;
  }

  if (!projects || projects.length === 0) {
    return (
      <EmptyState 
        icon={Folder} 
        title="No projects yet" 
        description="Get started by creating your first CodeMind project repository."
        action={<CreateProjectDialog />}
      />
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">Projects</h1>
          <p className="text-sm text-muted-foreground mt-1">Manage your connected repositories and workspaces.</p>
        </div>
        <CreateProjectDialog />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {projects.map((project: Project, index: number) => (
          <motion.div
            key={project.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2, ease: "easeOut", delay: index * 0.05 }}
          >
            <Link to={`/projects/${project.id}`} className="block h-full group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-xl">
              <Card className="h-full flex flex-col transition-all duration-200 hover:border-blue-accent/50 hover:shadow-md group-hover:bg-muted/30">
                <CardHeader className="flex-1 pb-4">
                  <div className="flex items-start justify-between">
                    <div className="w-10 h-10 rounded-lg bg-blue-accent/10 flex items-center justify-center text-blue-accent mb-3">
                      <Folder className="size-5" />
                    </div>
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="h-8 w-8 -mt-2 -mr-2 opacity-0 group-hover:opacity-100 transition-opacity"
                      onClick={(e) => {
                        e.preventDefault();
                        if (confirm('Are you sure you want to delete this project?')) {
                          deleteProject.mutate(project.id);
                        }
                      }}
                      title="Delete project"
                    >
                      <Trash2 className="size-4 text-red-500" />
                    </Button>
                  </div>
                  <CardTitle className="text-base truncate" title={project.name}>{project.name}</CardTitle>
                  <CardDescription className="line-clamp-2 mt-1.5 h-10" title={project.description || "No description provided."}>
                    {project.description || <span className="italic text-muted-foreground/60">No description provided.</span>}
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-0 text-xs text-muted-foreground flex items-center justify-between border-t border-border/50 pt-3 mt-auto">
                  <span>Updated {format(new Date(project.updated_at), "MMM d, yyyy")}</span>
                  <div className="flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                    Ready
                  </div>
                </CardContent>
              </Card>
            </Link>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
