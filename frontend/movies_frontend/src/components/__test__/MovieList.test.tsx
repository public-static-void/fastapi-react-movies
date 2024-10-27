import '@testing-library/jest-dom';
import { render, screen } from '../../test-utils';
import MovieList from '../MovieList';
import MockFormikContext from './MockFormikContext';

describe('Test MovieList', () => {
  beforeEach(() =>
    render(
      <MockFormikContext>
        <MovieList />
      </MockFormikContext>
    )
  );

  it('Loads the movies into the MovieList', async () => {
    const elementMovieTheGodfather = await screen.findByRole('option', {
      name: 'The Godfather',
    });
    expect(elementMovieTheGodfather).toBeInTheDocument();
  });
});
