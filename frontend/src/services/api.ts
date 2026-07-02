const BASE_URL = '/api';

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
  return fetchJson(`${BASE_URL}/projects`);
}

export function getProject(code: string): Promise<Project> {
  return fetchJson(`${BASE_URL}/projects/${code}`);
}

export function getProjectNotes(code: string): Promise<NoteItem[]> {
  return fetchJson(`${BASE_URL}/projects/${code}/notes`);
}

export function getProjectImages(code: string): Promise<ImageItem[]> {
  return fetchJson(`${BASE_URL}/projects/${code}/images`);
}

export function getProjectDocuments(code: string): Promise<DocumentItem[]> {
  return fetchJson(`${BASE_URL}/projects/${code}/documents`);
}

export function getProjectTeam(code: string): Promise<TeamMember[]> {
  return fetchJson(`${BASE_URL}/projects/${code}/team`);
}
