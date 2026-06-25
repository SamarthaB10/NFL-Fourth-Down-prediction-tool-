import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import FourthDowntool from "./pages/FourthDowntool";
import SimilarPlays from "./pages/SimilarPlays";
import TeamDashboard from "./pages/TeamDashboard";
import "./App.css";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="tool" element={<FourthDowntool />} />
          <Route path="plays" element={<SimilarPlays />} />
          <Route path="dashboard" element={<TeamDashboard />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
