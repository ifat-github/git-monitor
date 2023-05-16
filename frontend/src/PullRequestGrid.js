import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './grid.css';

const PullRequestGrid = () => {
  const [pullRequests, setPullRequests] = useState([]);

  useEffect(() => {
    const fetchPullRequests = async () => {
      try {
        const response = await axios.get('http://ec2-18-222-68-233.us-east-2.compute.amazonaws.com:5000/pullrequests');
        setPullRequests(response.data);
      } catch (error) {
        console.error('Error fetching pull requests:', error);
      }
    };

    fetchPullRequests();
  }, []);

  return (
    <div className="grid-container">
        <h1 className="grid-title">Pull Requests Monitor</h1>
        <table>
        <thead>
        <tr className="grid-header">
            <th>Action</th>
            <th>Number</th>
            <th>Title</th>
            <th>Author</th>
            <th>URL</th>
        </tr>
        </thead>
        <tbody>
        {pullRequests.map((item) => (
            <tr key={item.number} className="grid-row">
            <td>{item.action}</td>
            <td>{item.number}</td>
            <td>{item.title}</td>
            <td>{item.author}</td>
            <td>
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                {item.url}
                </a>
            </td>
            </tr>
        ))}
        </tbody>
        </table>
    </div>

  );
};

export default PullRequestGrid;
