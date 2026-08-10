import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2, Plus } from "lucide-react";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";

import { useCreateProject, projectCreateSchema, type ProjectCreate } from "../api/projectService";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog";

export function CreateProjectDialog() {
  const [open, setOpen] = useState(false);
  const createProject = useCreateProject();
  const navigate = useNavigate();

  const { register, handleSubmit, formState: { errors }, reset } = useForm<ProjectCreate>({
    resolver: zodResolver(projectCreateSchema),
  });

  const onSubmit = (data: ProjectCreate) => {
    createProject.mutate(data, {
      onSuccess: (project) => {
        toast.success("Project created successfully");
        setOpen(false);
        reset();
        navigate(`/projects/${project.id}`);
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || "Failed to create project");
      }
    });
  };

  const handleOpenChange = (newOpen: boolean) => {
    setOpen(newOpen);
    if (!newOpen) reset();
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button variant="primary" size="sm" className="gap-2">
          <Plus className="size-4" />
          New Project
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create New Project</DialogTitle>
          <DialogDescription>
            A project acts as a workspace for a specific codebase or repository.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-5 py-4">
          <div className="flex flex-col gap-2">
            <Label htmlFor="name">Project Name</Label>
            <Input 
              id="name" 
              placeholder="e.g., CodeMind Core" 
              disabled={createProject.isPending}
              {...register("name")}
            />
            {errors.name && <span className="text-xs text-red-500 font-medium">{errors.name.message}</span>}
          </div>
          
          <div className="flex flex-col gap-2">
            <Label htmlFor="description">Description (Optional)</Label>
            <Textarea 
              id="description" 
              placeholder="Briefly describe this repository..."
              disabled={createProject.isPending}
              {...register("description")}
            />
            {errors.description && <span className="text-xs text-red-500 font-medium">{errors.description.message}</span>}
          </div>
          
          <DialogFooter className="mt-4">
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => setOpen(false)}
              disabled={createProject.isPending}
            >
              Cancel
            </Button>
            <Button type="submit" variant="primary" disabled={createProject.isPending}>
              {createProject.isPending && <Loader2 className="mr-2 size-4 animate-spin" />}
              Create Project
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
