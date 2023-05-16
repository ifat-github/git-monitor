import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import PullRequestGrid from './PullRequestGrid';

jest.mock('axios'); // Mocking axios for testing purposes

describe('PullRequestGrid', () => {
  beforeEach(() => {
    // Mock the axios.get method to return sample data
    axios.get.mockResolvedValue({
      data: [
        {
          action: 'Opened',
          number: 1,
          title: 'Test Pull Request',
          author: 'John Doe',
          url: 'https://example.com/pr/1',
        },
      ],
    });
  });

  it('renders pull requests data', async () => {
    render(<PullRequestGrid />);

    expect(screen.getByText('Pull Requests Monitor')).toBeInTheDocument();

    // Wait for the data to be fetched and rendered
    await waitFor(() => {
      expect(screen.getByText('Opened')).toBeInTheDocument();
      expect(screen.getByText('1')).toBeInTheDocument();
      expect(screen.getByText('Test Pull Request')).toBeInTheDocument();
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('https://example.com/pr/1')).toBeInTheDocument();
    });
  });

  it('handles error in data fetching', async () => {
    // Mock axios.get to throw an error
    axios.get.mockRejectedValueOnce(new Error('Failed to fetch pull requests'));

    render(<PullRequestGrid />);

    expect(screen.getByText('Pull Requests Monitor')).toBeInTheDocument();

    // Wait for the error message to be displayed
    await waitFor(() => {
        const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
        expect(consoleSpy).toBeCalledTimes(1);
    });
  });
});
