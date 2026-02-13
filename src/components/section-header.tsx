"use client";

import { ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

interface SectionHeaderProps {
  id: string;
  title: string;
  icon?: React.ReactNode;
  collapsible?: boolean;
  defaultExpanded?: boolean;
  themeColor?: string;
  children: React.ReactNode;
  highlighted?: boolean;
}

export function SectionHeader({
  id,
  title,
  icon,
  collapsible = false,
  defaultExpanded = true,
  themeColor = "#2980b9",
  children,
  highlighted = false,
}: SectionHeaderProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <section
      id={id}
      className={`mb-8 scroll-mt-20 transition-all duration-300 ${
        highlighted ? 'ring-4 ring-offset-4 rounded-lg' : ''
      }`}
      style={highlighted ? { '--tw-ring-color': themeColor } as React.CSSProperties : {}}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          {icon && <div style={{ color: themeColor }}>{icon}</div>}
          <h2
            className="text-2xl md:text-3xl font-bold border-l-4 pl-4"
            style={{ borderColor: themeColor, color: themeColor }}
          >
            {title}
          </h2>
        </div>
        {collapsible && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center"
            aria-label={isExpanded ? "Collapse section" : "Expand section"}
            aria-expanded={isExpanded}
          >
            {isExpanded ? (
              <ChevronUp size={24} style={{ color: themeColor }} />
            ) : (
              <ChevronDown size={24} style={{ color: themeColor }} />
            )}
          </button>
        )}
      </div>
      {(!collapsible || isExpanded) && (
        <div className="animate-in fade-in-50 duration-300">
          {children}
        </div>
      )}
    </section>
  );
}
