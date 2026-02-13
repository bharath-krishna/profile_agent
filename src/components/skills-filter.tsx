"use client";

import { Search } from "lucide-react";
import { useState } from "react";

interface SkillCategory {
  name: string;
  skills: string[];
}

interface SkillsFilterProps {
  categories: SkillCategory[];
  themeColor?: string;
  activeCategory?: string;
  onCategoryChange?: (category: string) => void;
}

export function SkillsFilter({
  categories,
  themeColor = "#2980b9",
  activeCategory = "all",
  onCategoryChange,
}: SkillsFilterProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState(activeCategory);

  const handleCategoryClick = (category: string) => {
    setSelectedCategory(category);
    onCategoryChange?.(category);
  };

  const filteredCategories = categories.filter(cat => {
    if (selectedCategory !== "all" && cat.name !== selectedCategory) {
      return false;
    }
    if (searchTerm) {
      return cat.skills.some(skill =>
        skill.toLowerCase().includes(searchTerm.toLowerCase())
      ) || cat.name.toLowerCase().includes(searchTerm.toLowerCase());
    }
    return true;
  });

  const allCategories = ["all", ...categories.map(c => c.name)];

  return (
    <div className="space-y-6">
      {/* Search Bar */}
      <div className="relative">
        <Search
          className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
          size={20}
        />
        <input
          type="text"
          placeholder="Search skills..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:border-transparent text-base"
          style={{ '--tw-ring-color': themeColor } as React.CSSProperties}
        />
      </div>

      {/* Category Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {allCategories.map((category) => {
          const isActive = selectedCategory === category;
          return (
            <button
              key={category}
              onClick={() => handleCategoryClick(category)}
              className="px-4 py-2 rounded-full font-medium transition-all min-h-[44px] text-sm md:text-base capitalize"
              style={{
                backgroundColor: isActive ? themeColor : '#f3f4f6',
                color: isActive ? 'white' : '#374151',
              }}
            >
              {category}
            </button>
          );
        })}
      </div>

      {/* Skills Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCategories.map((category) => {
          const filteredSkills = category.skills.filter(skill =>
            !searchTerm || skill.toLowerCase().includes(searchTerm.toLowerCase())
          );

          if (filteredSkills.length === 0) return null;

          return (
            <div
              key={category.name}
              className="bg-gray-50 rounded-lg p-4 border-l-4"
              style={{ borderColor: themeColor }}
            >
              <h3
                className="font-semibold mb-3 text-base md:text-lg"
                style={{ color: themeColor }}
              >
                {category.name}
              </h3>
              <ul className="space-y-2">
                {filteredSkills.map((skill, index) => {
                  const isHighlighted =
                    searchTerm &&
                    skill.toLowerCase().includes(searchTerm.toLowerCase());
                  return (
                    <li
                      key={index}
                      className={`text-sm md:text-base ${
                        isHighlighted ? 'font-semibold' : 'text-gray-700'
                      }`}
                      style={isHighlighted ? { color: themeColor } : {}}
                    >
                      • {skill}
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })}
      </div>

      {filteredCategories.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No skills found matching your search.
        </div>
      )}
    </div>
  );
}
