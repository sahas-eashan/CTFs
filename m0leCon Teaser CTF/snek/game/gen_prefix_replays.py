actions = "WA.S..AWDW..A........WDSS..A...S..AWD".strip()
prefix_lengths = [1,6,16,22,30,34]
for idx,l in enumerate(prefix_lengths,1):
    with open(f"replay_prefix{idx}.txt","w") as f:
        f.write(actions[:l])
