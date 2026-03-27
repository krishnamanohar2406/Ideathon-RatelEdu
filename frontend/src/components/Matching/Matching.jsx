import React, { useEffect, useState } from 'react';
import Button from '../UI/Button';
import { Link } from 'react-router-dom';
import { matchesAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';

const Matching = () => {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    matchesAPI.list().then((res) => {
      setMatches(res.data);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex justify-center items-center h-64"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-50 p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent mb-4">
            Study Partner Matching
          </h1>
          <p className="text-xl text-gray-600">Find the perfect study buddy!</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-2xl p-8 shadow-xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Your Matches</h3>
            <p className="text-gray-600 mb-6">Matches filtered for you</p>
            <div className="space-y-3">
              {matches.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No matches yet. Create some connections!</p>
              ) : (
                matches.map((match) => (
                  <div key={match.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div>
                      <p className="font-semibold">{match.student1_name} ↔ {match.student2_name}</p>
                      <p className="text-sm text-gray-500">Status: <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        match.status === 'accepted' ? 'bg-green-100 text-green-800' :
                        match.status === 'rejected' ? 'bg-red-100 text-red-800' : 
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {match.status}
                      </span></p>
                    </div>
                    <Link to={`/matches/${match.id}`}>
                      <Button variant="secondary" size="sm">View</Button>
                    </Link>
                  </div>
                ))
              )}
            </div>
          </div>
          <div className="bg-gradient-to-br from-orange-500 to-pink-500 text-white rounded-2xl p-8 shadow-2xl">
            <h3 className="text-2xl font-bold mb-4">Ready to match?</h3>
            <p className="mb-6 opacity-90">Connect with students who share your study goals</p>
            <Button className="w-full" variant="secondary">Find New Matches</Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Matching;

