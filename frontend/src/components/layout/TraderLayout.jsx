import UserLayout from '../common/UserLayout';
import { traderNavigation } from '../../constants/navigation';

const TraderLayout = () => (
  <UserLayout
    role=\trader    colorFrom=\blue-500    colorTo=\purple-600    navigation={traderNavigation}
  />
);

export default TraderLayout;
