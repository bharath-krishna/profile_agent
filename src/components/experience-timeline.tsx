"use client";

import { ChevronDown, ChevronUp, Briefcase } from "lucide-react";
import { useState } from "react";

export interface ExperienceEntry {
  id: string;
  title: string;
  organization: string;
  period: string;
  description?: string;
  bullets?: string[];
  tech?: string;
  highlight?: boolean;
}

interface ExperienceTimelineProps {
  experiences: ExperienceEntry[];
  themeColor?: string;
  expandedId?: string | null;
  onExpand?: (id: string | null) => void;
}

export function ExperienceTimeline({
  experiences,
  themeColor = "#2980b9",
  expandedId: controlledExpandedId,
  onExpand,
}: ExperienceTimelineProps) {
  const [internalExpandedId, setInternalExpandedId] = useState<string | null>(
    experiences[0]?.id || null
  );

  const expandedId = controlledExpandedId !== undefined ? controlledExpandedId : internalExpandedId;

  const handleToggle = (id: string) => {
    const newId = expandedId === id ? null : id;
    if (onExpand) {
      onExpand(newId);
    } else {
      setInternalExpandedId(newId);
    }
  };

  return (
    <div className="space-y-4">
      {experiences.map((exp, index) => {
        const isExpanded = expandedId === exp.id;
        return (
          <div
            key={exp.id}
            id={exp.id}
            className={`bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300 scroll-mt-20 ${
              exp.highlight ? 'ring-2 ring-offset-2' : ''
            }`}
            style={exp.highlight ? { '--tw-ring-color': themeColor } as React.CSSProperties : {}}
          >
            {/* Header - Always Visible */}
            <button
              onClick={() => handleToggle(exp.id)}
              className="w-full p-6 text-left hover:bg-gray-50 transition-colors flex items-start gap-4"
              aria-expanded={isExpanded}
              aria-controls={`exp-content-${exp.id}`}
            >
              <div className="flex-shrink-0 pt-1">
                <Briefcase size={24} style={{ color: themeColor }} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-3 mb-2">
                  <h3
                    className="text-lg md:text-xl font-bold"
                    style={{ color: themeColor }}
                  >
                    {exp.title}
                  </h3>
                  <div className="flex-shrink-0">
                    {isExpanded ? (
                      <ChevronUp size={24} className="text-gray-400" />
                    ) : (
                      <ChevronDown size={24} className="text-gray-400" />
                    )}
                  </div>
                </div>
                <p className="text-gray-700 font-medium mb-1 text-sm md:text-base">
                  {exp.organization}
                </p>
                <p className="text-xs md:text-sm text-gray-500">{exp.period}</p>
              </div>
            </button>

            {/* Expandable Content */}
            {isExpanded && (
              <div
                id={`exp-content-${exp.id}`}
                className="px-6 pb-6 pt-2 animate-in fade-in-50 slide-in-from-top-2 duration-300"
              >
                {exp.description && (
                  <p className="text-gray-700 mb-4 text-sm md:text-base">
                    {exp.description}
                  </p>
                )}
                {exp.bullets && exp.bullets.length > 0 && (
                  <ul className="space-y-2 mb-4">
                    {exp.bullets.map((bullet, idx) => (
                      <li
                        key={idx}
                        className="flex items-start gap-2 text-sm md:text-base text-gray-700"
                      >
                        <span
                          className="mt-2 w-1.5 h-1.5 rounded-full flex-shrink-0"
                          style={{ backgroundColor: themeColor }}
                        />
                        <span>{bullet}</span>
                      </li>
                    ))}
                  </ul>
                )}
                {exp.tech && (
                  <div className="pt-3 border-t border-gray-200">
                    <span className="text-xs md:text-sm font-semibold text-gray-500 uppercase tracking-wide">
                      Tech Stack:
                    </span>
                    <p className="text-sm md:text-base mt-1 text-gray-700">
                      {exp.tech}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
