import React from "react";

export const Tab = ({ title, selected, onClick }) => {
  return (
    <div
      className={`tab ${selected ? "selected" : ""}`}
      onClick={onClick}
    >
      {title}
    </div>
  );
}