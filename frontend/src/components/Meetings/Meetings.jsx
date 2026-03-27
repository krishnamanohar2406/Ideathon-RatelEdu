import React, { useEffect, useState } from 'react';
import Button from '../UI/Button';
import { Link } from 'react-router-dom';
import { meetingsAPI } from '../../services/api';

const Meetings = () => {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    meetingsAPI.list().then((res) => {
      setMeetings(res.data);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex justify-center items-center h-64"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div></div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-50 p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-violet-600 bg-clip-text text-transparent mb-4">
            My Meetings
          </h1>
          <p className="text-xl text-gray-600">Scheduled study sessions</p>
        </header>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="p-8 border-b border-gray-100">
            <Button className="mr-4">Schedule New Meeting</Button>
            <Link to="/matching">
              <Button variant="secondary">Back to Matching</Button>
            </Link>
          </div>
          <div className="divide-y divide-gray-100">
            {meetings.length === 0 ? (
              <div className="p-20 text-center text-gray-500">
                <div className="w-24 h-24 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                  <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-2">No meetings scheduled</h3>
                <p>Find matches to schedule study sessions</p>
              </div>
            ) : (
              meetings.map((meeting) => (
                <div key={meeting.id} className="p-8 hover:bg-gray-50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                          meeting.status === 'completed' ? 'bg-green-100 text-green-800' :
                          meeting.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {meeting.status}
                        </span>
                        <span className="text-sm text-gray-500">Match ID: {meeting.match_id}</span>
                      </div>
                      <h3 className="text-xl font-bold text-gray-900 mb-1">Study Session</h3>
                      <p className="text-gray-600 mb-4">{meeting.participant_names.join(', ')}</p>
                      <div className="text-sm space-y-1">
                        <p><span className="font-medium">Time:</span> {new Date(meeting.start_time).toLocaleString()}</p>
                        {meeting.notes && <p><span className="font-medium">Notes:</span> {meeting.notes}</p>}
                      </div>
                    </div>
                    <Link to={`/meetings/${meeting.id}`} className="ml-4">
                      <Button size="sm" variant="secondary">Details</Button>
                    </Link>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Meetings;

