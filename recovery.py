from deadlock_detection import DeadlockDetector

class DeadlockRecovery:
    def __init__(self, detector):
        self.detector = detector

    def recover_from_deadlock(self):
        deadlock_cycle = self.detector.detect_deadlock()
        if deadlock_cycle:
            # Terminate the first process in the cycle
            process_to_terminate = deadlock_cycle[0][0]
            print(f"Terminating process {process_to_terminate} to break the deadlock.")
            self.detector.graph.remove_node(process_to_terminate)
        else:
            print("No deadlock to recover from.")
