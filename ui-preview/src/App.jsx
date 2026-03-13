import { useState } from "react";

import "../../ui/styles/tokens.css";
import "../../ui/styles/globals.css";
import "../../ui/styles/login.css";
import "../../ui/styles/products-categories.css";
import "../../ui/styles/super-admin.css";

import LoginPage from "../../ui/pages/LoginPage";
import ProductsCategoriesPage from "../../ui/pages/ProductsCategoriesPage";
import SuperAdminPage from "../../ui/pages/SuperAdminPage";

const pages = {
  login: "Login",
  products: "Produits et catégories",
  superAdmin: "Super Admin"
};

export default function App() {
  const [activePage, setActivePage] = useState("login");

  function renderPage() {
    if (activePage === "login") {
      return <LoginPage />;
    }

    if (activePage === "products") {
      return <ProductsCategoriesPage />;
    }

    if (activePage === "superAdmin") {
      return <SuperAdminPage />;
    }

    return <LoginPage />;
  }

  return (
    <div>
      <div style={previewBarStyle}>
        <div style={previewBarInnerStyle}>
          <div>
            <p style={previewLabelStyle}>Prévisualisation UI</p>
            <h1 style={previewTitleStyle}>Templates d’administration</h1>
          </div>

          <div style={previewActionsStyle}>
            <button
              type="button"
              onClick={() => setActivePage("login")}
              style={activePage === "login" ? activeButtonStyle : previewButtonStyle}
            >
              {pages.login}
            </button>

            <button
              type="button"
              onClick={() => setActivePage("products")}
              style={activePage === "products" ? activeButtonStyle : previewButtonStyle}
            >
              {pages.products}
            </button>

            <button
              type="button"
              onClick={() => setActivePage("superAdmin")}
              style={activePage === "superAdmin" ? activeButtonStyle : previewButtonStyle}
            >
              {pages.superAdmin}
            </button>
          </div>
        </div>
      </div>

      {renderPage()}
    </div>
  );
}

const previewBarStyle = {
  position: "sticky",
  top: 0,
  zIndex: 1000,
  background: "#ffffff",
  borderBottom: "1px solid #e2e8f0",
  padding: "16px 24px"
};

const previewBarInnerStyle = {
  maxWidth: "1280px",
  margin: "0 auto",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  gap: "16px",
  flexWrap: "wrap"
};

const previewLabelStyle = {
  margin: 0,
  fontSize: "0.85rem",
  fontWeight: 700,
  textTransform: "uppercase",
  letterSpacing: "0.08em",
  color: "#64748b"
};

const previewTitleStyle = {
  margin: "6px 0 0",
  fontSize: "1.5rem",
  color: "#0f172a"
};

const previewActionsStyle = {
  display: "flex",
  gap: "12px",
  flexWrap: "wrap"
};

const previewButtonStyle = {
  padding: "10px 14px",
  borderRadius: "12px",
  border: "1px solid #cbd5e1",
  background: "#ffffff",
  color: "#0f172a",
  fontWeight: 600,
  cursor: "pointer"
};

const activeButtonStyle = {
  ...previewButtonStyle,
  background: "#0f172a",
  color: "#ffffff",
  border: "1px solid #0f172a"
};
