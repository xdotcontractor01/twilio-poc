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
      <aside className="w-full md:w-72 shrink-0 border-b md:border-b-0 md:border-r border-gray-200 bg-gray-50">
        <div className="p-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Projects</h2>
          <p className="text-gray-400 text-sm">Loading projects...</p>
        </div>
      </aside>
    );
  }

  return (
    <aside className="w-full md:w-72 shrink-0 border-b md:border-b-0 md:border-r border-gray-200 bg-gray-50 md:overflow-y-auto">
      <div className="p-4 pb-2 md:pb-4">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Projects</h2>
      </div>
      <div className="flex md:flex-col gap-2 overflow-x-auto md:overflow-x-visible px-4 pb-4 md:px-4">
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
