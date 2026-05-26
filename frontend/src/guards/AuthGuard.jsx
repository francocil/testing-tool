import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

export default function AuthGuard({ children }) {
  const { access_token } = useSelector((state) => state.auth);

  if (!access_token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
