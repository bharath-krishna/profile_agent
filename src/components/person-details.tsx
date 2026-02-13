import { Person } from "@/lib/types";

// User icon for the person card
function UserIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="currentColor"
      className="w-16 h-16 text-indigo-600"
    >
      <path
        fillRule="evenodd"
        d="M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"
        clipRule="evenodd"
      />
    </svg>
  );
}

// Email icon
function EmailIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      fill="currentColor"
      className="w-4 h-4 text-gray-400"
    >
      <path d="M3 4a2 2 0 00-2 2v1.161l8.441 4.221a1.25 1.25 0 001.118 0L19 7.162V6a2 2 0 00-2-2H3z" />
      <path d="M19 8.839l-7.77 3.885a2.75 2.75 0 01-2.46 0L1 8.839V14a2 2 0 002 2h14a2 2 0 002-2V8.839z" />
    </svg>
  );
}

// Display a single field if it has a value
function PersonField({ label, value }: { label: string; value?: string | number }) {
  if (!value && value !== 0) return null;

  return (
    <div className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
      <span className="text-sm font-medium text-gray-500">{label}</span>
      <span className="text-sm text-gray-900 font-semibold">{value}</span>
    </div>
  );
}

export function PersonDetails({ person }: { person: Person }) {
  // Determine display name
  const displayName =
    person.name ||
    (person.firstName && person.lastName
      ? `${person.firstName} ${person.lastName}`
      : person.firstName || person.lastName || "Unknown Person");

  return (
    <div className="rounded-xl shadow-xl bg-white max-w-md w-full overflow-hidden">
      {/* Header with icon and name */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6">
        <div className="flex items-center space-x-4">
          <div className="bg-white/20 rounded-full p-3">
            <UserIcon />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-white">{displayName}</h3>
            {person.relationship && (
              <p className="text-indigo-100 text-sm mt-1">
                {person.relationship.replace(/_/g, " ")}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Details section */}
      <div className="p-6">
        <div className="space-y-1">
          <PersonField label="First Name" value={person.firstName} />
          <PersonField label="Last Name" value={person.lastName} />
          <PersonField label="Age" value={person.age} />
          <PersonField
            label="Gender"
            value={person.gender ? person.gender.charAt(0).toUpperCase() + person.gender.slice(1) : undefined}
          />

          {person.email && (
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <span className="text-sm font-medium text-gray-500 flex items-center">
                <EmailIcon />
                <span className="ml-2">Email</span>
              </span>
              <a
                href={`mailto:${person.email}`}
                className="text-sm text-indigo-600 hover:text-indigo-800 font-semibold"
              >
                {person.email}
              </a>
            </div>
          )}
        </div>

        {/* Metadata section (less prominent) */}
        {(person.exploration_depth !== undefined || person.is_complete !== undefined || person.last_updated) && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <p className="text-xs font-medium text-gray-400 mb-2">Metadata</p>
            <div className="space-y-1">
              {person.exploration_depth !== undefined && (
                <PersonField label="Exploration Depth" value={person.exploration_depth} />
              )}
              {person.is_complete !== undefined && (
                <PersonField label="Complete" value={person.is_complete ? "Yes" : "No"} />
              )}
              {person.last_updated && (
                <PersonField
                  label="Last Updated"
                  value={new Date(person.last_updated).toLocaleDateString()}
                />
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
