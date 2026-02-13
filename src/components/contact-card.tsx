"use client";

import { Mail, Phone, Globe, Copy, Download, Check } from "lucide-react";
import { useState } from "react";

interface ContactCardProps {
  email: string;
  phones: string[];
  website?: string;
  themeColor?: string;
}

export function ContactCard({
  email,
  phones,
  website,
  themeColor = "#2980b9",
}: ContactCardProps) {
  const [copiedItem, setCopiedItem] = useState<string | null>(null);

  const copyToClipboard = async (text: string, label: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedItem(label);
      setTimeout(() => setCopiedItem(null), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  const downloadVCard = () => {
    const vcard = `BEGIN:VCARD
VERSION:3.0
FN:Bharath Krishna
EMAIL:${email}
TEL;TYPE=CELL:${phones[0]}
${phones[1] ? `TEL;TYPE=CELL:${phones[1]}` : ''}
URL:${website || ''}
END:VCARD`;

    const blob = new Blob([vcard], { type: "text/vcard" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "bharath-krishna.vcf";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="space-y-4">
        {/* Email */}
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3 flex-1 min-w-0">
            <Mail size={20} style={{ color: themeColor }} className="flex-shrink-0" />
            <a
              href={`mailto:${email}`}
              className="text-gray-700 hover:underline truncate"
            >
              {email}
            </a>
          </div>
          <button
            onClick={() => copyToClipboard(email, "email")}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center flex-shrink-0"
            aria-label="Copy email"
          >
            {copiedItem === "email" ? (
              <Check size={18} style={{ color: themeColor }} />
            ) : (
              <Copy size={18} className="text-gray-600" />
            )}
          </button>
        </div>

        {/* Phones */}
        {phones.map((phone, index) => (
          <div key={index} className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3 flex-1 min-w-0">
              <Phone size={20} style={{ color: themeColor }} className="flex-shrink-0" />
              <a
                href={`tel:${phone}`}
                className="text-gray-700 hover:underline truncate"
              >
                {phone}
              </a>
            </div>
            <button
              onClick={() => copyToClipboard(phone, `phone-${index}`)}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center flex-shrink-0"
              aria-label="Copy phone number"
            >
              {copiedItem === `phone-${index}` ? (
                <Check size={18} style={{ color: themeColor }} />
              ) : (
                <Copy size={18} className="text-gray-600" />
              )}
            </button>
          </div>
        ))}

        {/* Website */}
        {website && (
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3 flex-1 min-w-0">
              <Globe size={20} style={{ color: themeColor }} className="flex-shrink-0" />
              <a
                href={website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-700 hover:underline truncate"
              >
                {website.replace(/^https?:\/\//, '')}
              </a>
            </div>
          </div>
        )}

        {/* Download vCard */}
        <div className="pt-4 border-t border-gray-200">
          <button
            onClick={downloadVCard}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg transition-colors min-h-[44px]"
            style={{
              backgroundColor: themeColor,
              color: 'white',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.opacity = '0.9';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.opacity = '1';
            }}
          >
            <Download size={18} />
            <span className="font-medium">Download Contact Card</span>
          </button>
        </div>
      </div>
    </div>
  );
}
