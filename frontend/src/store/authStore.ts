import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name?: string;
}

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  user: User | null;
  setAuth: (token: string, user: User) => void;
  logout: () => void;
}

// Check local storage for token on initialization
const initialToken = localStorage.getItem('codemind_access_token');

export const useAuthStore = create<AuthState>((set) => ({
  token: initialToken,
  isAuthenticated: !!initialToken,
  user: null, // Will be hydrated later via a /me endpoint if needed
  
  setAuth: (token, user) => {
    localStorage.setItem('codemind_access_token', token);
    set({ token, isAuthenticated: true, user });
  },
  
  logout: () => {
    localStorage.removeItem('codemind_access_token');
    set({ token: null, isAuthenticated: false, user: null });
  },
}));
