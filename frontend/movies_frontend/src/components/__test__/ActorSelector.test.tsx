import '@testing-library/jest-dom';
import { render, screen } from '../../test-utils';
import ActorSelector from '../ActorSelector';
import MockFormikContext from './MockFormikContext';
import { sawActors } from '../../mocks/defaults';

describe('Test ActorSelector', () => {
  beforeEach(() =>
    render(
      <MockFormikContext>
        <ActorSelector />
      </MockFormikContext>
    )
  );

  it('Loads the actors into the ActorSelector', async () => {
    for (const actor of sawActors) {
      expect(
        await screen.findByRole('option', { name: actor })
      ).toBeInTheDocument();
    }
  });

  it('Has the available actors listbox disabled on first load', async () => {
    expect(await screen.findByRole('listbox')).toBeDisabled();
  });

  it('Shows None for selected actors on first load', () => {
    expect(screen.getByRole('heading', { name: 'None' })).toBeInTheDocument();
  });
});
