import UserLayout from '../common/UserLayout';
import { affiliateNavigation } from '../../constants/navigation';

const AffiliateLayout = () => (
  <UserLayout
    role=\affiliate    colorFrom=\purple-500    colorTo=\pink-600    navigation={affiliateNavigation}
  />
);

export default AffiliateLayout;
