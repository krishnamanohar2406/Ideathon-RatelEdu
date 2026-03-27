import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import Button from '../UI/Button';
import api from '../../services/api';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [student, setStudent] = React.useState(null);

  React.useEffect(() => {
    api.get('/details/students/').then(res => {
      const myStudent = res.data.find(s => s.user === user.id);
      setStudent(myStudent);
    }).catch(console.error);
  }, [user]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50 p-8">
      <header className="max-w-6xl mx-auto flex justify-between items-center mb-12">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            RatelEdu Dashboard
          </h1>
          <p className="text-gray-600 mt-2">Welcome back, {user?.first_name}!</p>
        </div>
        <div className="flex gap-4">
          <Link to="/matching">
            <Button>Find Matches</Button>
          </Link>
          <Link to="/meetings">
            <Button variant="secondary">My Meetings</Button>
          </Link>
          <Button onClick={logout} variant="danger">Logout</Button>
        </div>
      </header>

      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1 bg-white rounded-2xl p-8 shadow-lg">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Profile</h2>
          {student ? (
            <div className="space-y-4">
              <p><span className="font-semibold">Name:</span> {student.name}</p>
              <p><span className="font-semibold">Email:</span> {student.email}</p>
              <p><span className="font-semibold">Phone:</span> {student.phone || 'Not set'}</p>
              <p><span className="font-semibold">TT Set:</span> {student.ttset}</p>
            </div>
          ) : (
            <p className="text-gray-500">Loading profile...</p>
          )}
        </div>
        <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link to="/profile" className="group">
            <div className="bg-gradient-to-r from-green-400 to-green-500 p-8 rounded-2xl text-white shadow-xl hover:shadow-2xl transition-all group-hover:scale-105">
              <h3 className="text-xl font-bold mb-2">Edit Profile</h3>
              <p>Update your student details</p>
            </div>
          </Link>
          <Link to="/matching" className="group">
            <div className="bg-gradient-to-r from-orange-400 to-orange-500 p-8 rounded-2xl text-white shadow-xl hover:shadow-2xl transition-all group-hover:scale-105">
              <h3 className="text-xl font-bold mb-2">Matching</h3>
              <p>Find study partners</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

