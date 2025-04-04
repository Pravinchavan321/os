class PageReplacement:
    def __init__(self, frame_size, reference_string):
        self.frame_size = frame_size
        self.reference_string = reference_string
        self.page_faults = 0

    def fifo(self):
        frame = []
        page_faults = 0
        for page in self.reference_string:
            if page not in frame:
                if len(frame) < self.frame_size:
                    frame.append(page)
                else:
                    frame.pop(0)
                    frame.append(page)
                page_faults += 1
        return page_faults

    def lru(self):
        frame = []
        page_faults = 0
        for page in self.reference_string:
            if page not in frame:
                if len(frame) < self.frame_size:
                    frame.append(page)
                else:
                    frame.pop(0)
                    frame.append(page)
                page_faults += 1
            else:
                frame.remove(page)
                frame.append(page) # Move to the most recently used
        return page_faults

    def optimal(self):
        frame = []
        page_faults = 0
        for i, page in enumerate(self.reference_string):
            if page not in frame:
                if len(frame) < self.frame_size:
                    frame.append(page)
                else:
                    future_use = {p: self.reference_string[i+1:].index(p) if p in self.reference_string[i+1:] else float('inf') for p in frame}
                    victim = max(future_use, key=future_use.get)
                    frame.remove(victim)
                    frame.append(page)
                page_faults += 1
        return page_faults