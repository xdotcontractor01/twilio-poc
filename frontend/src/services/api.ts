const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');

function apiUrl(path: string): string {
  return `${API_BASE_URL}/api${path}`;
}

export function getStorageUrl(filePath: string): string {
  if (filePath.startsWith('http://') || filePath.startsWith('https://')) {
    return filePath;
  }

  const parts = filePath.split('/storage/');
  if (parts.length > 1) {
    return `${API_BASE_URL}/storage/${parts[1]}`;
  }

  if (filePath.startsWith('/storage/')) {
    return `${API_BASE_URL}${filePath}`;
  }

  return filePath;
}

export interface Project {
  id: number;
  code: string;
  name: string;
  manager: string;
  contractor: string;
  status: string;
  completion_percentage: number;
}

export interface NoteItem {
  id: number;
  sender: string;
  message: string;
  created_at: string | null;
}

export interface ImageItem {
  id: number;
  filename: string;
  file_path: string;
  sender: string;
  created_at: string | null;
}

export interface DocumentItem {
  id: number;
  filename: string;
  file_path: string;
  sender: string;
  created_at: string | null;
}

export interface TeamMember {
  id: number;
  name: string;
  role: string;
}

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}

export function getProjects(): Promise<Project[]> {
  return fetchJson(apiUrl('/projects'));
}

export function getProject(code: string): Promise<Project> {
  return fetchJson(apiUrl(`/projects/${code}`));
}

export function getProjectNotes(code: string): Promise<NoteItem[]> {
  return fetchJson(apiUrl(`/projects/${code}/notes`));
}

export function getProjectImages(code: string): Promise<ImageItem[]> {
  return fetchJson(apiUrl(`/projects/${code}/images`));
}

export function getProjectDocuments(code: string): Promise<DocumentItem[]> {
  return fetchJson(apiUrl(`/projects/${code}/documents`));
}

export function getProjectTeam(code: string): Promise<TeamMember[]> {
  return fetchJson(apiUrl(`/projects/${code}/team`));
}
