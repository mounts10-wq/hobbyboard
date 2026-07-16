import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const { user } = useAuth();

  return (
    <section>
      <h1>Dashboard</h1>
      <p>Welcome, {user?.username}.</p>
      <p>Your hobby boards will appear here soon.</p>
    </section>
  );
}

export default Dashboard;