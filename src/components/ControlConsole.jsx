export default function ControlConsole() {
  return (
    <aside className="w-72 bg-oxidizedCopper p-4 flex flex-col space-y-6 border-r border-verdigris shadow-inner">
      {/* System Status (Animated Gauges) */}
      <section className="space-y-2">
        <h2 className="font-header text-brass text-lg">System Status</h2>
        <div className="flex space-x-4">
          {/* Example: Animated Gauge (could be SVG/d3 later) */}
          <div className="flex flex-col items-center bg-bronze rounded p-2 shadow-md w-20 h-20">
            <div className="text-neonTurquoise font-mono text-xl font-bold animate-pulse">78%</div>
            <small className="text-pumice">CPU Load</small>
          </div>
          <div className="flex flex-col items-center bg-bronze rounded p-2 shadow-md w-20 h-20">
            <div className="text-neonMagenta font-mono text-xl font-bold animate-pulse">43%</div>
            <small className="text-pumice">Memory</small>
          </div>
        </div>
      </section>

      {/* Navigation */}
      <section>
        <h2 className="font-header text-brass text-lg mb-2">Navigation</h2>
        <nav className="flex flex-col space-y-3">
          {['Dashboard', 'Protocols', 'Logs', 'Settings'].map(item => (
            <button key={item} className="bg-verdigris bg-opacity-20 hover:bg-verdigris rounded px-3 py-1 font-mono text-pumice transition">
              {item}
            </button>
          ))}
        </nav>
      </section>

      {/* Quick Tools */}
      <section>
        <h2 className="font-header text-brass text-lg mb-2">Quick Tools</h2>
        <div className="flex flex-col space-y-2">
          <button className="bg-neonTurquoise bg-opacity-20 text-neonTurquoise font-mono rounded px-3 py-1 shadow-inner hover:bg-opacity-40 transition">
            Qubit Readings
          </button>
          <button className="bg-neonMagenta bg-opacity-20 text-neonMagenta font-mono rounded px-3 py-1 shadow-inner hover:bg-opacity-40 transition">
            Pipette Calibrator
          </button>
        </div>
      </section>
    </aside>
  );
}
