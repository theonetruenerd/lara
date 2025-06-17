import { useState, useEffect } from 'react';

export default function AnimatedText({ text }) {
  const [displayed, setDisplayed] = useState('');

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setDisplayed(text.slice(0, i));
      i++;
      if (i > text.length) clearInterval(interval);
    }, 40);
    return () => clearInterval(interval);
  }, [text]);

  return (
    <div className="font-terminal whitespace-pre-wrap text-neonTurquoise drop-shadow-lg animate-flicker">
      {displayed}
      <span className="inline-block w-1 h-5 bg-neonTurquoise animate-pulse ml-1 align-bottom" />
    </div>
  );
}
