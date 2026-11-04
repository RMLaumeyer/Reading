import Shelf from './shelf';
// The local server serves exported files; catalog data loads in the browser.
export const dynamic = 'force-static';
export default function Home() {
  return <Shelf />;
}
