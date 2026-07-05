import { useCallback, useEffect, useRef, useState } from 'react';
import DocumentsPanel from './components/DocumentsPanel';
import ImagesPanel from './components/ImagesPanel';
import NotesPanel from './components/NotesPanel';
import ProjectHeader from './components/ProjectHeader';
import ProjectSidebar from './components/ProjectSidebar';
import SummaryPanel from './components/SummaryPanel';
import TeamPanel from './components/TeamPanel';
import type {
  DocumentItem,
  ImageItem,
  NoteItem,
  Project,
  TeamMember,
} from './services/api';
import {
  getProjectDocuments,
  getProjectImages,
  getProjectNotes,
  getProjectTeam,
  getProjects,
} from './services/api';

const POLL_INTERVAL = 5000;

export default function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedCode, setSelectedCode] = useState<string | null>(null);
  const [notes, setNotes] = useState<NoteItem[]>([]);
  const [images, setImages] = useState<ImageItem[]>([]);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [team, setTeam] = useState<TeamMember[]>([]);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedCodeRef = useRef(selectedCode);
  selectedCodeRef.current = selectedCode;

  const fetchProjects = useCallback(async () => {
    try {
      const data = await getProjects();
      setProjects(data);
      setError(null);
    } catch {
      setError('Unable to connect to the backend. Is the server running?');
    } finally {
      setLoadingProjects(false);
    }
  }, []);

  const fetchProjectDetails = useCallback(async (code: string) => {
    try {
      const [n, i, d, t] = await Promise.all([
        getProjectNotes(code),
        getProjectImages(code),
        getProjectDocuments(code),
        getProjectTeam(code),
      ]);
      if (selectedCodeRef.current === code) {
        setNotes(n);
        setImages(i);
        setDocuments(d);
        setTeam(t);
        setError(null);
      }
    } catch {
      setError('Failed to load project details.');
    } finally {
      setLoadingDetails(false);
    }
  }, []);

  useEffect(() => {
    fetchProjects();
    const interval = setInterval(fetchProjects, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchProjects]);

  useEffect(() => {
    if (!selectedCode) return;
    setLoadingDetails(true);
    fetchProjectDetails(selectedCode);
    const interval = setInterval(() => fetchProjectDetails(selectedCode), POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [selectedCode, fetchProjectDetails]);

  const handleSelect = (code: string) => {
    setSelectedCode(code);
    setNotes([]);
    setImages([]);
    setDocuments([]);
    setTeam([]);
  };

  const selectedProject = projects.find((p) => p.code === selectedCode) || null;

  return (
    <div className="min-h-screen flex flex-col bg-gray-100 overflow-x-hidden">
      <header className="bg-white border-b border-gray-200 px-4 py-3 md:px-6 md:py-4 shrink-0">
        <h1 className="text-lg md:text-xl font-bold text-gray-900">xDOT Field Hub</h1>
        <p className="text-xs md:text-sm text-gray-500">WhatsApp Project Communication Prototype</p>
      </header>

      {error && (
        <div className="bg-red-50 border-b border-red-200 px-4 py-3 md:px-6">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      <div className="flex flex-col md:flex-row flex-1 min-h-0">
        <ProjectSidebar
          projects={projects}
          selectedCode={selectedCode}
          onSelect={handleSelect}
          loading={loadingProjects}
        />

        <main className="flex-1 min-w-0 overflow-y-auto p-4 md:p-6">
          {!selectedProject ? (
            <div className="flex items-center justify-center min-h-[200px] md:min-h-full">
              <p className="text-gray-400 text-base md:text-lg text-center px-4">
                Select a project to view details
              </p>
            </div>
          ) : (
            <div className="w-full max-w-4xl mx-auto space-y-4">
              <ProjectHeader project={selectedProject} />
              <SummaryPanel
                notesCount={notes.length}
                imagesCount={images.length}
                documentsCount={documents.length}
              />
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <NotesPanel notes={notes} loading={loadingDetails} />
                <TeamPanel team={team} loading={loadingDetails} />
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <ImagesPanel images={images} loading={loadingDetails} />
                <DocumentsPanel documents={documents} loading={loadingDetails} />
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
