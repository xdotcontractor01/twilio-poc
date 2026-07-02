import type { TeamMember } from '../services/api';

interface Props {
  team: TeamMember[];
  loading: boolean;
}

export default function TeamPanel({ team, loading }: Props) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">Team</h3>
      {loading ? (
        <p className="text-sm text-gray-400">Loading...</p>
      ) : team.length === 0 ? (
        <p className="text-sm text-gray-400">No team members assigned.</p>
      ) : (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {team.map((member) => (
            <div key={member.id} className="flex items-center justify-between border-b border-gray-100 pb-2 last:border-0">
              <span className="text-sm text-gray-900">{member.name}</span>
              <span className="text-xs text-gray-500">{member.role}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
