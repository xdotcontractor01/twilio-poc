import type { ImageItem } from '../services/api';

interface Props {
  images: ImageItem[];
  loading: boolean;
}

function formatTime(ts: string | null): string {
  if (!ts) return '';
  return new Date(ts).toLocaleString();
}

function getImageUrl(filePath: string): string {
  const parts = filePath.split('/storage/');
  if (parts.length > 1) {
    return `/storage/${parts[1]}`;
  }
  return filePath;
}

export default function ImagesPanel({ images, loading }: Props) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">Images</h3>
      {loading ? (
        <p className="text-sm text-gray-400">Loading...</p>
      ) : images.length === 0 ? (
        <p className="text-sm text-gray-400">No images yet. Send an image via WhatsApp.</p>
      ) : (
        <div className="grid grid-cols-3 md:grid-cols-4 gap-2 max-h-64 overflow-y-auto">
          {images.map((img) => (
            <a
              key={img.id}
              href={getImageUrl(img.file_path)}
              target="_blank"
              rel="noopener noreferrer"
              className="block"
              title={`${img.sender} — ${formatTime(img.created_at)}`}
            >
              <img
                src={getImageUrl(img.file_path)}
                alt={img.filename}
                className="w-full h-20 object-cover rounded border border-gray-200 hover:border-blue-400"
              />
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
