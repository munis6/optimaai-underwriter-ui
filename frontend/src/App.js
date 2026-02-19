import React, { useState } from "react";
import "./App.css";
import UploadPanel from "./UploadPanel";
import BeforeAfterPanel from "./BeforeAfterPanel";
import PdfButton from "./PdfButton";

function App() {
  // ✅ FIXED — wrap payload ONCE
  async function callBackendEnrich(payload) {
    const res = await fetch("https://optimaai-underwriter-backend.onrender.com/enrich", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    return res.json();
  }

  const [rawJson, setRawJson] = useState(null);
  const [enrichedJson, setEnrichedJson] = useState(null);
  const [isEnriching, setIsEnriching] = useState(false);

  // ✅ FIXED — DO NOT double-wrap payload
  const handleFileSelect = async (file) => {
    const reader = new FileReader();

    reader.onload = async (event) => {
      try {
        const parsed = JSON.parse(event.target.result);

        setRawJson(parsed);
        setIsEnriching(true);

        try {
          const response = await callBackendEnrich(parsed); // FIXED
          setEnrichedJson(response.processed_data);
        } catch (err) {
          alert("Error contacting enrichment service.");
        }

        setIsEnriching(false);
      } catch (error) {
        alert("Invalid JSON file.");
      }
    };

    reader.readAsText(file);
  };

  const handleGeneratePdf = async () => {
    if (!enrichedJson) {
      alert("Please upload and enrich a JSON file first.");
      return;
    }

    try {
      const response = await fetch(
        "https://optimaai-underwriter-backend.onrender.com/generate-compliance-report",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(enrichedJson),
        }
      );

      if (!response.ok) {
        alert("PDF generation failed.");
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = "OptimaAI_Compliance_Report.pdf";
      link.click();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert("Error generating PDF.");
    }
  };

  return (
    <div className="app-container">
      <div className="header">OptimaAI Underwriter</div>

      <UploadPanel onFileSelect={handleFileSelect} />

      {isEnriching && (
        <div className="loading-banner">Enriching JSON… please wait</div>
      )}

      <BeforeAfterPanel rawJson={rawJson} enrichedJson={enrichedJson} />

      <PdfButton onGenerate={handleGeneratePdf} />
    </div>
  );
}

export default App;
