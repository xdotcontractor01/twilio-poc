import type { Project } from '../services/api';
import ProjectCard from './ProjectCard';

interface Props {
  projects: Project[];
  selectedCode: string | null;
  onSelect: (code: string) => void;
  loading: boolean;
}

export default function ProjectSidebar({ projects, selectedCode, onSelect, loading }: Props) {
  if (loading) {
    return (
      <aside className="w-72 border-r border-gray-200 p-4 overflow-y-auto bg-gray-50">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Projects</h2>
        <p className="text-gray-400 text-sm">Loading projects...</p>
      </aside>
    );
  }

  return (
    <aside className="w-72 border-r border-gray-200 p-4 overflow-y-auto bg-gray-50">
      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Projects</h2>
      <div className="space-y-2">
        {projects.map((project) => (
          <ProjectCard
            key={project.code}
            project={project}
            selected={project.code === selectedCode}
            onClick={() => onSelect(project.code)}
          />
        ))}
      </div>
    </aside>
  );
}
