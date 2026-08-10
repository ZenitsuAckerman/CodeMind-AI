import { api } from "@/lib/api";
import { z } from "zod";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

// Schemas
export const projectCreateSchema = z.object({
  name: z.string().min(1, "Name is required").max(100),
  description: z.string().max(1000).optional(),
});

export type ProjectCreate = z.infer<typeof projectCreateSchema>;

export interface Project {
  id: string;
  name: string;
  description: string | null;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

// API Calls
export const projectApi = {
  getProjects: async (): Promise<Project[]> => {
    const res = await api.get('/projects/');
    return res.data;
  },
  getProject: async (id: string): Promise<Project> => {
    const res = await api.get(`/projects/${id}`);
    return res.data;
  },
  createProject: async (data: ProjectCreate): Promise<Project> => {
    const res = await api.post('/projects/', data);
    return res.data;
  },
  deleteProject: async (id: string): Promise<void> => {
    await api.delete(`/projects/${id}`);
  }
};

// React Query Hooks
export const useProjects = () => {
  return useQuery({
    queryKey: ['projects'],
    queryFn: projectApi.getProjects,
  });
};

export const useProject = (id: string) => {
  return useQuery({
    queryKey: ['projects', id],
    queryFn: () => projectApi.getProject(id),
    enabled: !!id,
  });
};

export const useCreateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: projectApi.createProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });
};

export const useDeleteProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: projectApi.deleteProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });
};
