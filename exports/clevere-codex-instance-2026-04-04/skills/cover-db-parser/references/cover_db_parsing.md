# Devel::Cover DB Parsing Notes

This reference summarizes practical, low-risk ways to extract coverage details from a `cover_db/` directory.

## Prefer the `cover` CLI for quick answers

- Summary text:
  - `cover -report text`
- HTML summary:
  - `cover -report html_basic`
- Restrict to one file:
  - `cover -report text -select MSA/Shared/LdapAuth.pm`

These are the fastest ways to confirm statement/branch totals without custom parsing.

## When you need per-line or per-branch details

Use `cover -dump_db` to emit a Perl data structure that includes both:
- **Structure** (line numbers, branch expressions, etc.)
- **Counts** (how many times each statement/branch executed)

Command:

```bash
cover -dump_db > /tmp/cover_dump.txt
```

The dump includes two major hashes:
- `$structure` (describes where statements/branches are)
- `$db` (records counts by run and file)

### Key paths inside the dump

For a given file path (example: `shared/src/perl-lib/MSA/Shared/LdapAuth.pm`):

- **Statement line numbers**
  - `$structure->{f}{$file}{statement}` is an array of line numbers
- **Branch expressions**
  - `$structure->{f}{$file}{branch}` is an array of `[ line, { text => 'if (...)' } ]`
- **Counts for statements**
  - `$db->{runs}{$run_id}{count}{$file}{statement}` is an array of counts
- **Counts for branches**
  - `$db->{runs}{$run_id}{count}{$file}{branch}` is an array of pairs (true/false arm counts)

The structure arrays and count arrays are index-aligned. For example, the 12th entry in the
structure branch list corresponds to the 12th entry in the branch counts list.

## Safe parsing pattern

If you want to avoid brittle HTML parsing, parse the dump directly with a small Perl or Python script:

1. Run `cover -dump_db` and read the file.
2. Extract `$structure` and `$db` sections.
3. Use the index alignment to map counts to line numbers or branch expressions.

### Example (Perl pseudocode)

```perl
# Pseudocode: parse the dump, then correlate structure + counts
my $file = 'shared/src/perl-lib/MSA/Shared/LdapAuth.pm';
my $run_id = (keys %{$db->{runs}})[0];

my $stmt_lines = $structure->{f}{$file}{statement};
my $stmt_counts = $db->{runs}{$run_id}{count}{$file}{statement};

for my $i (0 .. $#$stmt_lines) {
  my $line = $stmt_lines->[$i];
  my $count = $stmt_counts->[$i];
  print "uncovered statement at line $line\n" if !$count;
}

my $branches = $structure->{f}{$file}{branch};
my $branch_counts = $db->{runs}{$run_id}{count}{$file}{branch};

for my $i (0 .. $#$branches) {
  my ($line, $meta) = @{$branches->[$i]};
  my ($true_count, $false_count) = @{$branch_counts->[$i]};
  if (!$true_count || !$false_count) {
    print "branch at line $line not fully covered: $meta->{text}\n";
  }
}
```

Notes:
- The exact run id is stored under `$db->{runs}`; use the first entry unless you intentionally ran multiple coverage sessions.
- Counts are numeric; treat `0` as uncovered.

## Devel::Cover::DB (programmatic access)

For direct API access, use `Devel::Cover::DB->new(db => 'cover_db')` and walk
`$db->cover->file($file)` with `statement`, `branch`, etc. If the API feels opaque,
`cover -dump_db` is usually faster and more transparent.

## Common pitfalls

- Ensure you’re parsing the same `cover_db` created by the test run you care about.
- Don’t assume HTML layouts are stable across Devel::Cover versions.
- Branch coverage often lags statement coverage; target missing branch arms first.
